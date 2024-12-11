describe('Recuperar Contraseña Page', () => {
    beforeEach(() => {
      cy.visit('http://localhost:3000/forgot-password'); 
      cy.wait(100);
    });
  
    it('should render the heading', () => {
      cy.get('h1.eSHwvX').should('exist').should('be.visible').contains('Recuperar contraseña');
    });
  
    it('should render the email input field', () => {
      cy.get('#email-input').should('exist').should('be.visible').should('have.attr', 'placeholder', 'Correo electrónico');
    });
  
    it('should render the reset password button', () => {
      cy.get('#reset-password-button').should('exist').should('be.visible').contains('Solicitar');
    });
  
    it('should render the return to login link', () => {
      cy.get('#login-return-link').should('exist').should('be.visible').contains('Volver');
    });
  
    it('should display a success message with valid email', () => {
      cy.get('#email-input').type('test@example.com');
      cy.get('#reset-password-button').click();
  
      cy.get('#success_alert').should('exist').should('be.visible').contains('Se ha enviado un correo.');
    });

    it('should not submit the form if email is invalid', () => {
        cy.get('#email-input').type('test.com');
        cy.get('#reset-password-button').click();
        cy.get('#error_alert').should('exist').should('be.visible').contains('Correo inválido.');
      });
  
  });