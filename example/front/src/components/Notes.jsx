'use client';

import { useState, useEffect } from 'react';
import { Trash2, Plus, Edit2, LogOut } from 'lucide-react';
import { useRouter } from 'next/navigation';
import { API_ENDPOINTS } from '@/lib/api';

export default function NotesGrid() {
  const router = useRouter();
  const [notes, setNotes] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editingNote, setEditingNote] = useState(null);
  const [formData, setFormData] = useState({
    title: '',
    content: '',
  });

  const [username, setUsername] = useState("");
  useEffect(() => {
      console.log("cookie", document.cookie);
      const match = document.cookie.match(/(?:^|; )username=([^;]*)/);
      const username = match ? decodeURIComponent(match[1]) : "";
      console.log(username);
      if (!username) router.replace("/login");
      setUsername(username); 
    }, [router]);


  useEffect(() => {
    fetchNotes();
  }, []);

  const fetchNotes = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(API_ENDPOINTS.NOTES.GET_ALL, {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Failed to fetch notes');
      }

      const data = await response.json();
      setNotes([...data]);
      setError('');
    } catch (err) {
      console.error(err);
      setError('Failed to load notes');
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleOpenModal = (note = null) => {
    if (note) {
      setEditingNote(note);
      setFormData({ title: note.title, content: note.content });
    } else {
      setEditingNote(null);
      setFormData({ title: '', content: '' });
    }
    setShowModal(true);
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setEditingNote(null);
    setFormData({ title: '', content: '' });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!formData.title.trim()) {
      setError('Title is required');
      return;
    }

    try {
      const endpoint = editingNote
        ? `${API_ENDPOINTS.NOTES.UPDATE}/${editingNote.id}`
        : API_ENDPOINTS.NOTES.CREATE;

      const method = editingNote ? 'PUT' : 'POST';

      const response = await fetch(endpoint, {
        method,
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error('Failed to save note');
      }

      await fetchNotes();
      handleCloseModal();
    } catch (err) {
      console.error(err);
      setError('Failed to save note');
    }
  };

  const handleDelete = async (noteId) => {
    if (!confirm('Are you sure you want to delete this note?')) {
      return;
    }

    try {
      const response = await fetch(`${API_ENDPOINTS.NOTES.DELETE}/${noteId}`, {
        method: 'DELETE',
        credentials: 'include',
      });

      if (!response.ok) {
        throw new Error('Failed to delete note');
      }

      await fetchNotes();
    } catch (err) {
      console.error(err);
      setError('Failed to delete note');
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 via-purple-100 to-blue-100 p-8">
      {/* Logout Button - top right */}
      <button
        onClick={() => router.push('/logout')}
        title="Logout"
        className="fixed right-6 top-6 z-50 bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg shadow-md flex items-center gap-2 transition-transform duration-150 transform hover:scale-105"
      >
        <LogOut className="w-4 h-4" />
        Logout
      </button>
      {/* <h1 >//className="fixed right-6 top-6 z-50 bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded-lg shadow-md flex items-center gap-2 transition-transform duration-150 transform hover:scale-105"> */}
      <h1>
      {username}
      </h1>

      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-12">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">My Notes</h1>
          <p className="text-gray-600">Organize your thoughts and ideas</p>
        </div>

        {/* Error Message */}
        {error && (
          <div className="mb-6 bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
            <p className="text-red-700 text-sm font-medium">{error}</p>
          </div>
        )}

        {/* Create Note Button */}
        <button
          onClick={() => handleOpenModal()}
          className="mb-8 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white font-bold py-3 px-6 rounded-xl transition-all duration-200 transform hover:scale-105 active:scale-95 shadow-lg flex items-center gap-2"
        >
          <Plus className="w-5 h-5" />
          Create Note
        </button>

        {/* Loading State */}
        {isLoading ? (
          <div className="flex items-center justify-center py-12">
            <div className="w-12 h-12 border-4 border-blue-200 border-t-blue-500 rounded-full animate-spin"></div>
          </div>
        ) : notes.length === 0 ? (
          /* Empty State */
          <div className="bg-white rounded-3xl shadow-2xl p-12 text-center backdrop-blur-sm bg-opacity-95">
            <div className="mb-4">
              <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Plus className="w-8 h-8 text-blue-500" />
              </div>
            </div>
            <h2 className="text-2xl font-bold text-gray-800 mb-2">No notes yet</h2>
            <p className="text-gray-600 mb-6">Create your first note to get started</p>
            <button
              onClick={() => handleOpenModal()}
              className="inline-block bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white font-bold py-3 px-8 rounded-xl transition-all duration-200 transform hover:scale-105 active:scale-95 shadow-lg"
            >
              Create First Note
            </button>
          </div>
        ) : (
          /* Notes Grid */
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {notes?.map((note) => (
              <div
                key={note.id}
                className="bg-white rounded-3xl shadow-2xl p-6 backdrop-blur-sm bg-opacity-95 hover:shadow-xl transition-all duration-200 transform hover:scale-105 flex flex-col h-full group"
              >
                {/* Note Header */}
                <div className="flex items-start justify-between mb-4">
                  <h3 className="text-xl font-bold text-gray-800 flex-1 break-words line-clamp-2">
                    {note.title}
                  </h3>
                  <div className="flex gap-2 ml-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button
                      onClick={() => handleOpenModal(note)}
                      className="p-2 text-blue-500 hover:bg-blue-50 rounded-lg transition-colors"
                      title="Edit note"
                    >
                      <Edit2 className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => handleDelete(note.id)}
                      className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                      title="Delete note"
                    >
                      <Trash2 className="w-5 h-5" />
                    </button>
                  </div>
                </div>

                {/* Note Content */}
                <p className="text-gray-600 flex-1 line-clamp-4 mb-4 break-words">
                  {note.content || 'No content'}
                </p>

                {/* Note Footer */}
                <div className="text-xs text-gray-400 pt-4 border-t border-gray-200">
                  {new Date(note.createdAt).toLocaleDateString()}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-3xl shadow-2xl p-8 w-full max-w-md backdrop-blur-sm bg-opacity-95">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">
              {editingNote ? 'Edit Note' : 'Create Note'}
            </h2>

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Title Input */}
              <div>
                <label htmlFor="title" className="block text-sm font-semibold text-gray-700 mb-2">
                  Title
                </label>
                <input
                  id="title"
                  type="text"
                  name="title"
                  value={formData.title}
                  onChange={handleChange}
                  placeholder="Note title"
                  required
                  className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-blue-500 focus:outline-none transition-colors bg-gray-50 placeholder-gray-400"
                />
              </div>

              {/* Content Input */}
              <div>
                <label htmlFor="content" className="block text-sm font-semibold text-gray-700 mb-2">
                  Content
                </label>
                <textarea
                  id="content"
                  name="content"
                  value={formData.content}
                  onChange={handleChange}
                  placeholder="Write your note here..."
                  rows="6"
                  className="w-full px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-blue-500 focus:outline-none transition-colors bg-gray-50 placeholder-gray-400 resize-none"
                />
              </div>

              {/* Buttons */}
              <div className="flex gap-4">
                <button
                  type="button"
                  onClick={handleCloseModal}
                  className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 font-bold py-3 rounded-xl transition-all duration-200"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="flex-1 bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 text-white font-bold py-3 rounded-xl transition-all duration-200 transform hover:scale-105 active:scale-95"
                >
                  {editingNote ? 'Update' : 'Create'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

