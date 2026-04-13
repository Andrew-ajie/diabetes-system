/**
 * Shared date/time utilities for the patient uni-app.
 */

/**
 * Returns the current local datetime formatted as "YYYY-MM-DDTHH:mm",
 * suitable for pre-filling datetime input fields.
 */
export function formatLocalISO(date = new Date()) {
  const pad = (n) => String(n).padStart(2, '0');
  return (
    `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}` +
    `T${pad(date.getHours())}:${pad(date.getMinutes())}`
  );
}
