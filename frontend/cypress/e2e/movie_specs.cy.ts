describe('MovieDetails Page with API Calls', () => {
    beforeEach(() => {
      // Intercept the API calls
      cy.intercept('POST', '**/rest/v1/rpc/get_movie_details').as('getMovieDetails');
      cy.intercept('POST', '**/rest/v1/rpc/get_movie_genres').as('getGenres');
      cy.intercept('POST', '**/rest/v1/rpc/get_movie_cast').as('getCast');
      cy.intercept('POST', '**/rest/v1/rpc/get_movie_director').as('getDirector');
      cy.intercept('POST', '**/rest/v1/rpc/get_movie_language').as('getLanguage');
  
      // Visit the MovieDetails page with a sample movie ID
      cy.visit('http://localhost:3000/movies/buscando-a-nemo?id=12'); // Adjust the URL if needed
    });
  
    it('should load movie details correctly with API calls', () => {
      // Wait for all the necessary API calls to complete
      cy.wait('@getMovieDetails');
      cy.wait('@getGenres');
      cy.wait('@getCast');
      cy.wait('@getDirector');
      cy.wait('@getLanguage');
  
      cy.get('#movie-title').should('be.visible').and('contain.text', 'Buscando a Nemo'); 

      // Check correct poster
      cy.get('#movie-release-rating').should('be.visible').and('contain.text', '2003-05-30'); // Replace with actual release date
      cy.get('#movie-release-rating').should('contain.text', 'Rating:'); // Ensure 'Rating' label is present
  
      // Check if the movie poster is visible
      cy.get('#movie-poster').should('be.visible');
  
      // Check if the movie overview is visible
      cy.get('#movie-overview').should('be.visible').and('contain.text', 'Nemo, un pececillo, hijo único muy querido y protegido por su padre, ha sido capturado en un arrecife australiano y ahora vive en una pecera en la oficina de un dentista de Sidney. El tímido padre de Nemo se embarcará en una peligrosa aventura para rescatar a su hijo. Pero Nemo y sus nuevos amigos tienen también un astuto plan para escapar de la pecera y volver al mar.'); // Replace with actual content
  
      // Check if the "Forum" button exists and is clickable
      cy.get('#forum-button').should('be.visible').and('be.enabled').and('contain.text', 'Foro');
  
      // Check if the movie information section is visible
      cy.get('#movie-info').should('be.visible');
  
      // Check if the director's name is displayed
      cy.get('#director-name').should('contain.text', 'Andrew Stanton'); 
  
      // Check if the cast list is populated
      cy.get('#cast-list').children().should('have.length.greaterThan', 0); // Ensure there are cast members listed
  
      // Check if the movie's genre is displayed
      cy.get('#genre-list').children().should('have.length.greaterThan', 0); // Ensure there are genres listed
  
      // Check if the language is displayed
      cy.get('#language-name').should('contain.text', 'Inglés');
  
      // Check if the release date is correct
      cy.get('#release-date').should('contain.text', '2003-05-30'); 
    });
  
    it('should navigate to the forum when the button is clicked', () => {
      // Simulate clicking the "Forum" button
      cy.get('#forum-button').click();
  
      // Verify that the user is redirected to the correct page
      // You can replace '/forum' with the actual forum route
      cy.url().should('include', '/forum');
    });
  });
  