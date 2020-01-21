# Changelog

All notable changes to this project will be documented in this file.

## [2.1.0] - Jan x, 2020

### Added
- OpenAPI Swagger Documentation, available at `/api`
- New `PlagiarismSerializer`
- Email API. Currently available email APIs.
	- Plagiarism Report (Report Students for plagiarism)
	- Report Question (Sends e-mail to professor for improving the question with student feedback)
	- Anonymous Website Feedback (Provide feedback to creators) with option for providing user e-mail.
- Token Auth

### Removed
- Old API Documentation end-point `api-docs`.


## [2.0.0] - Jan 18, 2020

### Added

- New `utilities` app for housing different services like code evaluation, plagiarism, e-mail etc.
- Support for new languages `PHP` & `Bash`.
- New model for holding Moss Plagiarism results (For Future Use).
- Add `created_date` in **Assignment**, **Question** & **Classroom** model.
- Fixed a bug where a new file was saved every time a solution was submitted, (`OverwriteStorage()` in **Solution** Model).
- New `moss_id` field in **Professor** model.
- Support for Plagiarism Services (powered by Moss).

### Changed
- Submission path, the solutions are now saved inside `/media/submissions/assignments/<assg_id>/` with name like `<question-id>_<student_id>`.
- `profile_pic` and `instistution` fields now accept `null` while signing up for a new user.
- Default submission status is now set to _Not Attempted_.
- Renamed `Python` to `Python3`.
- `marks` field in **Question** model is now `null` acceptable.
- Only 1 Submission per student, **Solution** now relates to Student by `OneToOne` relation.
- `PATCH`/`DELETE` options for Classroom, Assignment, Questions & Submissions.


## [1.0.0] - Nov 27, 2019
- Initial Release