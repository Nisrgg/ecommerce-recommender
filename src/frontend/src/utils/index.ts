// Utility functions for the frontend application

import { clsx, type ClassValue } from 'clsx';

/**
 * Combines class names using clsx
 */
export function cn(...inputs: ClassValue[]) {
  return clsx(inputs);
}

/**
 * Formats a date string to a readable format
 */
export function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  });
}

/**
 * Truncates text to a specified length
 */
export function truncateText(text: string, maxLength: number): string {
  if (text.length <= maxLength) return text;
  return text.slice(0, maxLength) + '...';
}

/**
 * Debounces a function call
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: NodeJS.Timeout;
  return (...args: Parameters<T>) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => func(...args), wait);
  };
}

/**
 * Generates a random ID
 */
export function generateId(): string {
  return Math.random().toString(36).substr(2, 9);
}

/**
 * Validates if a string is a valid number
 */
export function isValidNumber(value: string): boolean {
  const num = Number(value);
  return !isNaN(num) && isFinite(num) && num > 0;
}

/**
 * Formats a number with commas
 */
export function formatNumber(num: number): string {
  return num.toLocaleString();
}

/**
 * Capitalizes the first letter of a string
 */
export function capitalize(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

/**
 * Converts a string to kebab-case
 */
export function kebabCase(str: string): string {
  return str
    .replace(/([a-z])([A-Z])/g, '$1-$2')
    .replace(/[\s_]+/g, '-')
    .toLowerCase();
}

/**
 * Checks if the current environment is development
 */
export function isDevelopment(): boolean {
  return import.meta.env.DEV;
}

/**
 * Checks if the current environment is production
 */
export function isProduction(): boolean {
  return import.meta.env.PROD;
}

/**
 * Gets the API base URL from environment variables
 */
export function getApiBaseUrl(): string {
  return import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
}

/**
 * Sleeps for a specified number of milliseconds
 */
export function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * Retries a function a specified number of times
 */
export async function retry<T>(
  fn: () => Promise<T>,
  retries: number = 3,
  delay: number = 1000
): Promise<T> {
  try {
    return await fn();
  } catch (error) {
    if (retries > 0) {
      await sleep(delay);
      return retry(fn, retries - 1, delay);
    }
    throw error;
  }
}

