// lib/api.js

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000/api/base';
const API_AUTH_URL = process.env.NEXT_AUTH_API_URL || 'http://localhost:4000/api/auth';
export const API_ENDPOINTS = {
  // Auth endpoints
  AUTH: {
    LOGIN: `${API_AUTH_URL}/login/`,
    SIGNUP: `${API_AUTH_URL}/signup/`,
    LOGOUT: `${API_AUTH_URL}/logout/`,
    TOTP: `${API_AUTH_URL}/confirm-totp/`,
    // REFRESH_TOKEN: `${API_BASE_URL}/auth/refresh`,
    // FORGOT_PASSWORD: `${API_BASE_URL}/auth/forgot-password`,
    // RESET_PASSWORD: `${API_BASE_URL}/auth/reset-password`,
  },
  NOTES: {
    GET_ALL: `${API_BASE_URL}/notes`,
    UPDATE: `${API_BASE_URL}/notes`,
    CREATE: `${API_BASE_URL}/notes`,
    DELETE: `${API_BASE_URL}/notes`,
  },

  // // User endpoints
  // USER: {
  //   GET_PROFILE: `${API_BASE_URL}/user/profile`,
  //   UPDATE_PROFILE: `${API_BASE_URL}/user/profile`,
  //   DELETE_ACCOUNT: `${API_BASE_URL}/user/account`,
  //   GET_SETTINGS: `${API_BASE_URL}/user/settings`,
  //   UPDATE_SETTINGS: `${API_BASE_URL}/user/settings`,
  // },

  // // Posts endpoints
  // POSTS: {
  //   GET_ALL: `${API_BASE_URL}/posts`,
  //   GET_BY_ID: (id) => `${API_BASE_URL}/posts/${id}`,
  //   CREATE: `${API_BASE_URL}/posts`,
  //   UPDATE: (id) => `${API_BASE_URL}/posts/${id}`,
  //   DELETE: (id) => `${API_BASE_URL}/posts/${id}`,
  // },

  // // Comments endpoints
  // COMMENTS: {
  //   GET_BY_POST: (postId) => `${API_BASE_URL}/posts/${postId}/comments`,
  //   CREATE: (postId) => `${API_BASE_URL}/posts/${postId}/comments`,
  //   DELETE: (commentId) => `${API_BASE_URL}/comments/${commentId}`,
  // },
};

export default API_ENDPOINTS;

