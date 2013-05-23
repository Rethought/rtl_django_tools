RTL Django Tools
================

A repository of generalised tools and models that the ReThought find useful.

User model
==========

Keen to have a user  model that relied only upon email address as the
primary identifier and not have any reference to the redundant 
`username` field, we created `rtl_django_tools.models.User`.

Used with Django>=1.5 this provides a user model that is identical in all
respects to the default User model with the exception of no username field
and the email having a unique constraint.

For those wishing to build upon this, implement your own extensions by
sub-classing `rtl_django_tools.models.AbstractBasicUser`.
