describe('MovieDetails API Integration Tests', () => {
  beforeEach(() => {
    // Interceptar las llamadas a las API relacionadas con los detalles de la película
    cy.intercept('POST', '**/rest/v1/rpc/get_movie_details').as('getMovieDetails');
    cy.intercept('POST', '**/rest/v1/rpc/get_movie_genres').as('getGenres');
    cy.intercept('POST', '**/rest/v1/rpc/get_movie_cast').as('getCast');
    cy.intercept('POST', '**/rest/v1/rpc/get_movie_director').as('getDirector');
    cy.intercept('POST', '**/rest/v1/rpc/get_movie_language').as('getLanguage');

    // Navegar a la página con un ID de muestra
    cy.visit('http://localhost:3000/movies/buscando-a-nemo?id=12'); // Ajustar URL si es necesario
  });

  it('should fetch and verify movie details from the API', () => {
    cy.wait('@getMovieDetails').then((interception) => {
      expect(interception.response.statusCode).to.eq(200); // Código de éxito
      const movieDetails = interception.response.body;

      // Verificar detalles de la película
      expect(movieDetails[0].title).to.equal('Buscando a Nemo');
      expect(movieDetails[0].release_date).to.equal('2003-05-30');
    });

    cy.wait('@getGenres').then((interception) => {
      expect(interception.response.statusCode).to.eq(200);
      const genres = interception.response.body;

      // Verificar que existen géneros
      expect(genres).to.have.length.greaterThan(0);
    });

    cy.wait('@getCast').then((interception) => {
      expect(interception.response.statusCode).to.eq(200);
      const cast = interception.response.body;

      // Verificar que el reparto está poblado
      expect(cast).to.have.length.greaterThan(0);
    });

    cy.wait('@getDirector').then((interception) => {
      expect(interception.response.statusCode).to.eq(200);
      const director = interception.response.body;

      // Verificar el nombre del director
      expect(director[0].director_name).to.equal('Andrew Stanton');
    });

    cy.wait('@getLanguage').then((interception) => {
      expect(interception.response.statusCode).to.eq(200);
      const language = interception.response.body;

      // Verificar el idioma de la película
      expect(language[0].language_name).to.equal('Inglés');
    });
  });

  it('should navigate to the forum when requested', () => {
      cy.intercept('POST', '**/rest/v1/rpc/exists_forum').as('checkForumExist');
      cy.visit('http://localhost:3000/movies/buscando-a-nemo/forum?id=12');
      cy.wait('@checkForumExist').its('response.statusCode').should('eq', 200);
  });
});
