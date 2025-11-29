This module implements generic CRUD views for Book using Django REST Framework.
- ListView: Public read-only access for all books.
- DetailView: Public read-only access for a specific book.
- CreateView, UpdateView, DeleteView: Restricted to authenticated users.
- Custom methods (perform_create, perform_update) allow extension of logic.
- Permissions ensure secure and role-based access.
