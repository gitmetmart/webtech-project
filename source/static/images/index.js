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

  /**
   * Bewerkt een notitie op basis van het opgegeven notitie-ID en de nieuwe inhoud.
   * @param {number} noteId - Het ID van de notitie die bewerkt moet worden.
   * @param {string} newContent - De nieuwe inhoud van de notitie.
   */
  function editNote(noteId, newContent) {
    fetch("/edit-note", {
      method: "POST",
      body: JSON.stringify({ noteId: noteId, newContent: newContent }),
    }).then((_res) => {
      window.location.href = "/";
    });
  }