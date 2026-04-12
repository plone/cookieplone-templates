context('Example Acceptance Tests', () => {
  describe('Visit a page', () => {
    beforeEach(() => {
      // Given a logged in editor
      cy.viewport('macbook-16');
      cy.createContent({
        contentType: 'Document',
        contentId: 'document',
        contentTitle: 'Test document',
        transition: 'publish',
      });
      cy.autologin();
    });

    it('As editor I can add visit a Page', function () {
      cy.visit('/document');
    });
  });
});
