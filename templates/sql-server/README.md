# SQL Server Templates

This directory contains SQL Server templates for MDAN-AUTO projects.

## Templates

### Database Schema Template
- `schema.sql` - Basic database schema template
- `stored-procedures.sql` - Common stored procedures
- `functions.sql` - User-defined functions
- `views.sql` - Common views
- `triggers.sql` - Audit and validation triggers

### Migration Template
- `migration-template.sql` - SQL migration template with versioning

### Performance Templates
- `indexes.sql` - Index optimization scripts
- `queries.sql` - Common query patterns

## Usage

```bash
# Copy schema template
cp templates/sql-server/schema.sql my-project/database/

# Run migration
sqlcmd -S localhost -d mydb -i migration-template.sql
```

## Best Practices

- Always use parameterized queries
- Include error handling in stored procedures
- Use transactions for multi-step operations
- Add indexes for frequently queried columns
- Implement audit logging