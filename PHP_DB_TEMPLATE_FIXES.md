# PHP Database Templates - Fixes and Improvements

## Completed Fixes

1. **Fixed PostgreSQL Connectivity**

   - Updated `bootstrap.php` to properly detect container environment variables
   - Fixed port handling to use internal container ports (5432 for PostgreSQL, 3306 for MySQL/MariaDB)
   - Added PDO PostgreSQL driver to PHP Dockerfile

2. **MariaDB Template Fixes**

   - Fixed port mapping issues with MariaDB template
   - Ensured consistent environment variable names between containers
   - Added proper MariaDB-specific environment variables

3. **Landing Page Improvements**

   - Enhanced the landing page template to dynamically detect database type
   - Added better diagnostic information for connection failures
   - Improved dynamic port detection for all database types

4. **DSN Connection Strings**
   - Updated PDO connection strings to use dynamic port detection
   - Fixed PostgreSQL `pgsql:` connection string format
   - Consolidated database version detection code

## Remaining Issues

1. **Port Mapping Link Mismatches**
   - The landing page still shows incorrect port information for PostgreSQL template
   - pgAdmin link should point to port 8081 but shows 8082

## Proposed Next Steps

1. **Template Environment Testing**

   - Create a test script to validate all template variants (MySQL, MariaDB, PostgreSQL)
   - Implement automatic port mapping verification

2. **Documentation Updates**

   - Update README.md with database template information
   - Document database environment variables

3. **Port Variable Standardization**

   - Create consistent naming conventions for environment variables across templates
   - Ensure template_manager.py sets all needed environment variables

4. **Tooling Admin Links**
   - Fix the admin tool links (phpMyAdmin vs pgAdmin) to correctly display the right ports

## Future Enhancements

1. **Multiple Database Support**

   - Add support for using multiple databases in a single stack
   - Implement database selection during project creation

2. **Database Migration Templates**

   - Add basic migration templates for common frameworks
   - Include sample data seeding for demo purposes

3. **Connection Testing**

   - Add automated connection testing to show detailed error information
   - Implement retry logic for slow-starting database containers

4. **Database Plugin System**
   - Move database functionality to plugins (for v0.3.0)
   - Allow adding databases to existing projects
