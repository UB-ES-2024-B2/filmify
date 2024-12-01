describe('Forum Page Functional Tests', () => {
  describe('Forum Loading State', () => {
    it('should make the API request to check forum loading state', () => {
      // Interceptar las peticiones de carga del foro
      cy.intercept('POST', '**/rest/v1/rpc/exists_forum').as('checkForumExist');
      cy.intercept('POST', '**/rest/v1/rpc/get_forum_info').as('fetchForumInfo');

      cy.visit('http://localhost:3000/movies/buscando-a-nemo/forum?id=12');

      // Esperar las peticiones
      cy.wait('@checkForumExist').its('response.statusCode').should('eq', 200);
      cy.wait('@fetchForumInfo').its('response.statusCode').should('eq', 200);
    });
  });

  // Test Case 2: Forum Existence Check when Unlogged
  describe('Forum Unlogged Exist State', () => {
    beforeEach(() => {
      // Interceptar las peticiones API
      cy.intercept('POST', '**/rest/v1/rpc/exists_forum').as('checkForumExist');
      cy.intercept('POST', '**/rest/v1/rpc/get_forum_info').as('fetchForumInfo');
      cy.visit('http://localhost:3000/movies/buscando-a-nemo/forum?id=12'); // Ajustar la URL
    });

    it('should verify the forum exists and retrieve the correct forum information', () => {
      // Esperar las peticiones y asegurarse de que se recibieron correctamente
      cy.wait('@checkForumExist').its('response.statusCode').should('eq', 200);
      cy.wait('@fetchForumInfo').then((interception) => {
        // Verificar el código de estado de la solicitud
        expect(interception.response.statusCode).to.eq(200);
        // Verificar que los datos del foro sean los correctos
        const forumData = interception.response.body;  // Obtener la respuesta de la API
        console.log(forumData)
        expect(forumData[0].name).to.equal('Buscando a Nemo Foro');
        expect(forumData[0].description).to.equal('Publicar post para la comunidad de esta película.');
      });
    });
  });
});
