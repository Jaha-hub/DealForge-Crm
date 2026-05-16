import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

// Intl formatter instances are cached by locale key to avoid repeated
// object allocation on every call (hot path in lists/tables).
const dateFormatterCache = new Map<string, Intl.DateTimeFormat>()
const dateTimeFormatterCache = new Map<string, Intl.DateTimeFormat>()
const currencyFormatterCache = new Map<string, Intl.NumberFormat>()

function getDateFormatter(locale: string): Intl.DateTimeFormat {
  let fmt = dateFormatterCache.get(locale)
  if (!fmt) {
    fmt = new Intl.DateTimeFormat(locale, {
      timeZone: "Asia/Tashkent",
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    })
    dateFormatterCache.set(locale, fmt)
  }
  return fmt
}

function getDateTimeFormatter(locale: string): Intl.DateTimeFormat {
  let fmt = dateTimeFormatterCache.get(locale)
  if (!fmt) {
    fmt = new Intl.DateTimeFormat(locale, {
      timeZone: "Asia/Tashkent",
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    })
    dateTimeFormatterCache.set(locale, fmt)
  }
  return fmt
}

function getCurrencyFormatter(currency: string): Intl.NumberFormat {
  let fmt = currencyFormatterCache.get(currency)
  if (!fmt) {
    fmt = new Intl.NumberFormat("ru-UZ", {
      style: "currency",
      currency,
      minimumFractionDigits: 0,
    })
    currencyFormatterCache.set(currency, fmt)
  }
  return fmt
}

export function formatDate(date: string | Date, locale = "ru-RU"): string {
  return getDateFormatter(locale).format(new Date(date))
}

export function formatDateTime(date: string | Date, locale = "ru-RU"): string {
  return getDateTimeFormatter(locale).format(new Date(date))
}

export function formatCurrency(amount: number, currency = "UZS"): string {
  return getCurrencyFormatter(currency).format(amount)
}
