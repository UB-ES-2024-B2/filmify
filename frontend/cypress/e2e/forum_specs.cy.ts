describe('Forum Page Tests', () => {

    // Test Case 1: Forum Loading State
    describe('Forum Loading State', () => {
      it('should show the loading message when the forum is loading', () => {
        cy.visit('http://localhost:3000/movies/buscando-a-nemo/forum?id=12'); // Adjust the URL path
        cy.get('#loading-forum').should('be.visible');
        cy.get('#forum-exists').should('not.exist');
        cy.get('#forum-not-available').should('not.exist');
      });
    });


    describe('Forum Unlogged Exist State', () => {
        beforeEach(() => {
          cy.intercept('POST', '**/rest/v1/rpc/exists_forum').as('checkForumExist');
          cy.intercept('POST', '**/rest/v1/rpc/get_forum_info').as('fetchForumInfo');
          cy.visit('http://localhost:3000/movies/buscando-a-nemo/forum?id=12'); // Adjust the URL path
        });
      
        it('should display forum details when the forum exists', () => {
          cy.wait('@checkForumExist');
          cy.wait('@fetchForumInfo');
          
          cy.get('#forum-exists').should('be.visible');
          cy.get('#forum-header').should('be.visible');
          cy.get('#forum-name').should('have.text', 'Buscando a Nemo Foro');
          cy.get('#forum-description').should('have.text', 'Publicar post para la comunidad de esta película.');
          cy.get('#post-button').should('not.exist');
        });
      });
      
  
  });
  