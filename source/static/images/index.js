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

  // JavaScript
function editNote(noteId) {
  var newData = prompt("Enter new note data:");
  if (newData) {
      $.post("/update_note", {id: noteId, data: newData}, function(response) {
          if (response.success) {
              // Update the note in the UI
              // This will depend on how your HTML is structured
              $("#note" + noteId).text(newData);
          } else {
              alert("Failed to update note.");
          }
      });
  }
}