function mapSelect(name, id, diffName, stars, bpm, username) {
  const data = {
  map_name: name,
  map_id: id,
  difficulty_name: diffName,
  stars: stars,
  bpm: bpm,
  player_host: username
  }
  fetch('/matchmaking/', {
  method: 'POST', 
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data),
  })
}