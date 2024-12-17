describe('Home Page with API Calls', () => {
    beforeEach(() => {
      // Intercept the API calls
      cy.intercept('POST', '**/rest/v1/rpc/get_popular_movies').as('getPopular');
      cy.intercept('POST', '**/rest/v1/rpc/get_newest_movies').as('getNewest');
  
      // Visit the MovieDetails page with a sample movie ID
      cy.visit('http://localhost:3000/'); // Adjust the URL if needed
    });

    it('should render the main page layout', () => {
        cy.get('#main-page').should('exist').should('be.visible');
    });
    
    it('should render the "Nuevas" section', () => {
    cy.wait('@getNewest');
    cy.get('#newest-section').should('exist').should('be.visible');
    cy.get('#newest-carousel').should('exist').should('be.visible');
    });

    it('should render the "Populares" section', () => {
    cy.wait('@getPopular');
    cy.get('#newest-section').should('exist').should('be.visible');
    cy.get('#popular-carousel').should('exist').should('be.visible');
    });
    
});