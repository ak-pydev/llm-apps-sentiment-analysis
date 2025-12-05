import { client } from './client';

export interface Review {
  id: string;
  app_name: string;
  rating: number;
  sentiment: string;
  text: string;
  created_at: string;
}

export const reviewsAPI = {
  getAll: async () => {
    return client.get<Review[]>('/reviews');
  },

  getByApp: async (appName: string) => {
    return client.get<Review[]>(`/reviews?app_name=${appName}`);
  },

  getTopReviews: async (limit: number = 10) => {
    return client.get<Review[]>(`/reviews/top?limit=${limit}`);
  },
};
