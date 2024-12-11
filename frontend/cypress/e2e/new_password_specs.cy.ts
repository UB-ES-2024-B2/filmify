describe('Reestablecer Contraseña Page', () => {
    beforeEach(() => {
      cy.visit('http://localhost:3000/new-password'); // Adjust the URL if needed
      cy.wait(100);
    });
  
    it('should render the heading', () => {
      cy.get('#new-password-heading')
        .should('exist')
        .should('be.visible')
        .contains('Reestablece tu contraseña');
    });
  
    it('should render the new password input field', () => {
      cy.get('#new-password-input')
        .should('exist')
        .should('be.visible')
        .should('have.attr', 'placeholder', 'Nueva contraseña');
    });
  
    it('should render the confirm password input field', () => {
      cy.get('#confirm-password-input')
        .should('exist')
        .should('be.visible')
        .should('have.attr', 'placeholder', 'Reescribe contraseña');
    });
  
    it('should render the save password button', () => {
      cy.get('#save-password-button')
        .should('exist')
        .should('be.visible')
        .contains('Guardar');
    });
  
    it('should display an error when passwords do not match', () => {
      cy.get('#new-password-input').type('Password123!');
      cy.get('#confirm-password-input').type('Password456!');
      cy.get('#save-password-button').click();
      cy.get('#error').should('exist').should('be.visible').contains('Contraseñas no coinciden');
    });
  
    it('should display an error message when the API returns an error', () => {
  
      cy.get('#new-password-input').type('Password123!');
      cy.get('#confirm-password-input').type('Password123!');
      cy.get('#save-password-button').click();
  
      // Error since we dont have a token.
      cy.get('#error').should('exist').should('be.visible').contains('Error');
    });

  });
  