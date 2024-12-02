describe('Login Page', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000/login'); // Adjust the URL if needed
    cy.wait(100);
  });

  it('should render the login heading', () => {
    cy.get('#login-heading').should('exist').should('be.visible');
  });

  it('should render the email input field', () => {
    cy.get('#email-input').should('exist').should('be.visible');
  });

  it('should render the password input field', () => {
    cy.get('#password-input').should('exist').should('be.visible');
  });

  it('should render the login button', () => {
    cy.get('#login-button').should('exist').should('be.visible');
  });

  it('should render the forgot password link', () => {
    cy.get('#forgot-password-link').should('exist').should('be.visible');
  });

  it('should render the register link', () => {
    cy.get('#register-link').should('exist').should('be.visible');
  });

  it('should submit the form when valid credentials are entered', () => {
    cy.get('#email-input').type('test@example.com');
    cy.get('#password-input').type('password123');
    cy.get('#login-button').click();
  });
});
