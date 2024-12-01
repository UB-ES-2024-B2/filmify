describe('Register Page', () => {
    beforeEach(() => {
      cy.visit('http://localhost:3000/register'); // Visit the register page
      cy.wait(100); // Optional: Wait for the page to fully load
    });
  
    it('should render the register heading', () => {
      cy.get('#register-heading')
        .should('exist')
        .should('be.visible')
        .should('contain.text', 'Regístrate');
    });
  
    it('should render the username input field', () => {
      cy.get('#username-input')
        .should('exist')
        .should('be.visible')
        .should('have.attr', 'placeholder', 'Usuario');
    });
  
    it('should render the email input field', () => {
      cy.get('#email-input')
        .should('exist')
        .should('be.visible')
        .should('have.attr', 'placeholder', 'Correo');
    });
  
    it('should render the password input field', () => {
      cy.get('#password-input')
        .should('exist')
        .should('be.visible')
        .should('have.attr', 'placeholder', 'Contraseña');
    });
  
    it('should render the create account button', () => {
      cy.get('#create-account-button')
        .should('exist')
        .should('be.visible')
        .should('contain.text', 'Crear cuenta');
    });
  
    it('should render the login link', () => {
      cy.get('#login-link')
        .should('exist')
        .should('be.visible')
        .should('contain.text', 'Iniciar sesión');
    });
  
    it('should submit the form when valid credentials are entered', () => {
      cy.get('#username-input').clear().type('testuser');
      cy.get('#email-input').clear().type('testuser@example.com');
      cy.get('#password-input').clear().type('TestPassword123');
      cy.get('#create-account-button', { timeout: 10000 }).click();
      // Add your assertions here to verify the success behavior (e.g., redirect, success message)
    });
  
    it('should display an error message if username is missing', () => {
      cy.get('#username-input').clear().type('testuser').clear();
      cy.get('#email-input').clear().type('testuser@example.com');
      cy.get('#password-input').clear().type('TestPassword123');
      cy.get('.field-error').should('exist').should('contain.text', 'El nombre de usuario es requerido.'); 
    });

    it('should display an error message if email is invalid', () => {
      cy.get('#username-input').clear().type('testuser');
      cy.get('#email-input').clear().type('invalidemail');
      cy.get('#password-input').clear().type('TestPassword123'); 
      cy.get('.field-error').should('exist').should('contain.text', 'El correo electrónico no es válido.'); 
    });

    it('should display an error message if password is not 8 characters long', () => {
        cy.get('#username-input').clear().type('testuser');
        cy.get('#email-input').clear().type('testuser@example.com');
        cy.get('#password-input').clear().type('Test'); 
        cy.get('.field-error').should('exist').should('contain.text', 'La contraseña debe tener al menos 8 caracteres'); 
      });
  });
  