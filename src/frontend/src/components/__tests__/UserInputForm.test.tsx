// Tests for UserInputForm component

import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import UserInputForm from '../UserInputForm';

describe('UserInputForm', () => {
  const mockOnSubmit = jest.fn();

  beforeEach(() => {
    mockOnSubmit.mockClear();
  });

  it('renders correctly', () => {
    render(<UserInputForm onSubmit={mockOnSubmit} loading={false} />);
    
    expect(screen.getByText('Find Recommendations')).toBeInTheDocument();
    expect(screen.getByLabelText('User ID')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /get recommendations/i })).toBeInTheDocument();
  });

  it('shows sample user buttons', () => {
    render(<UserInputForm onSubmit={mockOnSubmit} loading={false} />);
    
    expect(screen.getByText('User 1')).toBeInTheDocument();
    expect(screen.getByText('User 5')).toBeInTheDocument();
    expect(screen.getByText('User 10')).toBeInTheDocument();
    expect(screen.getByText('User 15')).toBeInTheDocument();
    expect(screen.getByText('User 20')).toBeInTheDocument();
  });

  it('validates empty input', async () => {
    const user = userEvent.setup();
    render(<UserInputForm onSubmit={mockOnSubmit} loading={false} />);
    
    const submitButton = screen.getByRole('button', { name: /get recommendations/i });
    await user.click(submitButton);
    
    expect(screen.getByText('Please enter a valid user ID')).toBeInTheDocument();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('validates invalid input', async () => {
    const user = userEvent.setup();
    render(<UserInputForm onSubmit={mockOnSubmit} loading={false} />);
    
    const input = screen.getByLabelText('User ID');
    const submitButton = screen.getByRole('button', { name: /get recommendations/i });
    
    await user.type(input, 'abc');
    await user.click(submitButton);
    
    expect(screen.getByText('Please enter a valid number')).toBeInTheDocument();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('validates range', async () => {
    const user = userEvent.setup();
    render(<UserInputForm onSubmit={mockOnSubmit} loading={false} />);
    
    const input = screen.getByLabelText('User ID');
    const submitButton = screen.getByRole('button', { name: /get recommendations/i });
    
    await user.type(input, '100');
    await user.click(submitButton);
    
    expect(screen.getByText('User ID must be between 1 and 50')).toBeInTheDocument();
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  it('submits valid input', async () => {
    const user = userEvent.setup();
    render(<UserInputForm onSubmit={mockOnSubmit} loading={false} />);
    
    const input = screen.getByLabelText('User ID');
    const submitButton = screen.getByRole('button', { name: /get recommendations/i });
    
    await user.type(input, '5');
    await user.click(submitButton);
    
    expect(mockOnSubmit).toHaveBeenCalledWith(5);
  });

  it('handles sample user clicks', async () => {
    const user = userEvent.setup();
    render(<UserInputForm onSubmit={mockOnSubmit} loading={false} />);
    
    const sampleButton = screen.getByText('User 10');
    await user.click(sampleButton);
    
    expect(mockOnSubmit).toHaveBeenCalledWith(10);
    expect(screen.getByDisplayValue('10')).toBeInTheDocument();
  });

  it('shows loading state', () => {
    render(<UserInputForm onSubmit={mockOnSubmit} loading={true} />);
    
    expect(screen.getByText('Getting Recommendations...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /getting recommendations/i })).toBeDisabled();
  });

  it('disables sample buttons when loading', () => {
    render(<UserInputForm onSubmit={mockOnSubmit} loading={true} />);
    
    const sampleButtons = screen.getAllByRole('button', { name: /user \d+/i });
    sampleButtons.forEach(button => {
      expect(button).toBeDisabled();
    });
  });

  it('clears error when input changes', async () => {
    const user = userEvent.setup();
    render(<UserInputForm onSubmit={mockOnSubmit} loading={false} />);
    
    const input = screen.getByLabelText('User ID');
    const submitButton = screen.getByRole('button', { name: /get recommendations/i });
    
    // Trigger error
    await user.click(submitButton);
    expect(screen.getByText('Please enter a valid user ID')).toBeInTheDocument();
    
    // Clear error by typing
    await user.type(input, '5');
    expect(screen.queryByText('Please enter a valid user ID')).not.toBeInTheDocument();
  });

  it('handles form submission with Enter key', async () => {
    const user = userEvent.setup();
    render(<UserInputForm onSubmit={mockOnSubmit} loading={false} />);
    
    const input = screen.getByLabelText('User ID');
    
    await user.type(input, '5');
    await user.keyboard('{Enter}');
    
    expect(mockOnSubmit).toHaveBeenCalledWith(5);
  });
});

