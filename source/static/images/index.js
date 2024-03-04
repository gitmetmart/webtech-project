/**
 * Verwijdert een notitie op basis van het opgegeven notitie-ID.
 * @param {number} noteId - Het ID van de notitie die verwijderd moet worden.
 */
//Javasript voor de home pagina
function deleteNote(noteId) {
    fetch("/delete-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }
