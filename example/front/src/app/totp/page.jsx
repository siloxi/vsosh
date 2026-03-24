'use client';

import { useState } from 'react';
import { API_ENDPOINTS } from '@/lib/api';
import { ShieldCheck, RefreshCw } from 'lucide-react';

export default function TotpForm() {
  const [code, setCode] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [resendLoading, setResendLoading] = useState(false);

  const submitTotp = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setIsLoading(true);

    try {
      const res = await fetch(API_ENDPOINTS.AUTH.TOTP, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ code: code.trim() }),
      });

      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body?.message || 'TOTP verification failed');
      }

      setSuccess('Verified — redirecting…');
      window.location.href = '/';
    } catch (err) {
      console.error(err);
      setError(err?.message || 'Invalid code');
    } finally {
      setIsLoading(false);
    }
  };

  const resendTotp = async () => {
    setError('');
    setSuccess('');
    setResendLoading(true);

    try {
      const res = await fetch(API_ENDPOINTS.AUTH.RESEND_TOTP, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
      });

      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body?.message || 'Resend failed');
      }

      setSuccess('A new code was sent.');
    } catch (err) {
      console.error(err);
      setError(err?.message || 'Could not resend code');
    } finally {
      setResendLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 via-purple-100 to-blue-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">Two‑Factor Authentication</h1>
          <p className="text-gray-600">Enter the 6‑digit code from your authenticator app</p>
        </div>

        <div className="bg-white rounded-3xl shadow-2xl p-8 backdrop-blur-sm bg-opacity-95">
          <form onSubmit={submitTotp} className="space-y-6">
            <div>
              <label htmlFor="totp" className="block text-sm font-semibold text-gray-700 mb-2">
                Authentication code
              </label>
              <input
                id="totp"
                type="text"
                inputMode="numeric"
                pattern="\d{6}"
                maxLength={6}
                value={code}
                onChange={(e) => setCode(e.target.value.replace(/\D/g, '').slice(0, 6))}
                placeholder="000000"
                required
                className="w-full text-center tracking-widest text-xl px-4 py-3 rounded-xl border-2 border-gray-200 focus:border-blue-500 focus:outline-none transition-colors bg-gray-50 placeholder-gray-400"
              />
              {/* <p className="text-xs text-gray-500 mt-2">Use your authenticator app (Google Authenticator, Authy, etc.).</p> */}
            </div>

            {error && (
              <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded-lg">
                <p className="text-red-700 text-sm font-medium">{error}</p>
              </div>
            )}

            {success && (
              <div className="bg-green-50 border-l-4 border-green-500 p-4 rounded-lg">
                <p className="text-green-700 text-sm font-medium flex items-center gap-2">
                  <ShieldCheck className="w-4 h-4" /> {success}
                </p>
              </div>
            )}

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-blue-500 to-purple-500 hover:from-blue-600 hover:to-purple-600 disabled:opacity-50 disabled:cursor-not-allowed text-white font-bold py-3 rounded-xl transition-all duration-200 transform hover:scale-105 active:scale-95 shadow-lg"
            >
              {isLoading ? (
                <span className="flex items-center justify-center gap-2">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  Verifying...
                </span>
              ) : (
                'Verify'
              )}
            </button>
          </form>

          {/* <div className="mt-6 flex items-center justify-between"> */}
            {/* <button */}
              {/* type="button" */}
              {/* onClick={resendTotp} */}
              {/* disabled={resendLoading} */}
              {/* className="inline-flex items-center gap-2 text-sm text-blue-500 hover:text-blue-600 font-medium transition-colors" */}
            {/* > */}
              {/* {resendLoading ? ( */}
                {/* <span className="flex items-center gap-2"> */}
                  {/* <div className="w-4 h-4 border-2 border-blue-500 border-t-transparent rounded-full animate-spin" /> */}
                  {/* Resending... */}
                {/* </span> */}
              {/* ) : ( */}
                {/* <> */}
                  {/* <RefreshCw className="w-4 h-4" /> Resend code */}
                {/* </> */}
              {/* )} */}
            {/* </button> */}

            {/* <a href="/login" className="text-sm text-gray-600 hover:text-gray-800"> */}
              {/* Back to sign in */}
            {/* </a> */}
          {/* </div> */}

          {/* <div className="mt-6 relative"> */}
            {/* <div className="absolute inset-0 flex items-center"> */}
              {/* <div className="w-full border-t border-gray-200"></div> */}
            {/* </div> */}
            {/* <div className="relative flex justify-center text-sm"> */}
              {/* <span className="px-2 bg-white text-gray-500">security</span> */}
            {/* </div> */}
          {/* </div> */}

          {/* <p className="text-center text-gray-600 mt-6 text-xs"> */}
            {/* // If you lost access to your authenticator app, contact support. */}
          {/* </p> */}
        </div>

        {/* <p className="text-center text-gray-600 text-xs mt-6"> */}
          {/* // By using 2FA you help keep your account secure. */}
        {/* </p> */}
      </div>
    </div>
  );
}
