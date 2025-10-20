import React from 'react';
import { render, screen } from '@testing-library/react';
import { Header } from './Header';

test('renders the header with the correct title', () => {
  render(<Header />);
  
  // Check for the logo/brand name
  const brandElement = screen.getByText(/React \+ Bun \+ K8s/i);
  expect(brandElement).toBeInTheDocument();
});
