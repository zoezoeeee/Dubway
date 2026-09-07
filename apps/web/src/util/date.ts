export function isWeekendInDublin() {
  const day = new Intl.DateTimeFormat("en-IE", {
    timeZone: "Europe/Dublin",
    weekday: "short",
  }).format(new Date());

  return day === "Sat" || day === "Sun";
}

export function formatDublinDate() {
  const date = new Intl.DateTimeFormat("en-IE", {
    day: "numeric",
    month: "short",
    timeZone: "Europe/Dublin",
    weekday: "long",
  }).format(new Date());

  const time = new Intl.DateTimeFormat("en-IE", {
    hour: "2-digit",
    hour12: false,
    minute: "2-digit",
    timeZone: "Europe/Dublin",
  }).format(new Date());

  return `${date} · ${time}`;
}
