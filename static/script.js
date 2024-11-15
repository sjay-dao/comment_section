function upvote(commentId) {
    fetch(`/upvote/${commentId}`, {
      method: 'POST'
    })
    .then(response => response.json())
    .then(data => {
      const upvoteCountElement = document.getElementById(`upvote-count-${commentId}`);
      upvoteCountElement.textContent = `(${data.upvote_count})`;
    })
    .catch(error => {
      console.error('Error upvoting:', error);
      // Handle error, e.g., display an error message
    });
  }