Jobsboard website built with Django for the backend and Bootstrap for the frontend.

# FEATURES:
- The project uses a Postgresql database, you can configure your preferred database on the settings.py.
- Responsive navbar with the relevant menu.
- There are two user types, during user registration a user gets to choose between 'candidate' and 'employer', with either of the two having different privileges:

    A candidate:
    * can log in after a successful registration
    * can edit their profile(profile pic, bio). The profile is created automatically after a successful registration.
    * can access the jobs section, see all available jobs, apply for jobs that match their skills and qualifications, either internally(inside the jobs website itself) or externally(through a link to the potential employer's website). No duplicate applications allowed.


    An employer:
    * can log in after a successful registration
    * can create a company profile through which they can post jobs
    * can edit both the personal and the company profiles
    * can post jobs related to the company profile
    * can only view, edit and delete jobs which they have posted, and can view successful applicants for each specific job.
    * can add, edit and delete testimonials and also view the existing testimonials

- The Jobs section has filters, based on the industry in which the jobs fall under, the job-type, experience level and when the job was posted.
- The Jobs section also has a search functionality based on keyword and location.

Blog section
- A blog can be created on the admin panel by a superuser and an existing user assigned as the author.
- Logged in users can comment on the blog. Users can also reply to the comments to a blog

