import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders the main application title', () => {
  render(<App />);
  const titleElement = screen.getByText(/Welcome to the Future/i);
  expect(titleElement).toBeInTheDocument();
});
