async function loadMealsFromAPI(search = "") {
  const response = await fetch(`/api/meals/?search=${encodeURIComponent(search)}`);
  if (!response.ok) throw new Error("API request failed");
  return response.json();
}
