# Changelog

All notable changes to this project will be documented in this file.

## [1.1.0] - Jan x, 2020

### Added

- New `utilities` app for housing different services like code evaluation, plagiarism, e-mail etc.
- Support for new languages `PHP` & `Bash`.
- New model for holding Moss Plagiarism results (**PlagResult**).
- Add `created_date` in **Assignment**, **Question** & **Classroom** model.
- Fixed a bug where a new file was saved every time a solution was submitted, (`OverwriteStorage()` in **Solution** Model).
- Add `moss_id` field in **Professor** model.

### Changed
- Submission path, the solutions are now saved inside `/media/submissions/assignments/<assg_id>/` with name like `<question-id>_<student_id>`.
- `profile_pic` and `instistution` fields now accept `null` while signing up for a new user.
- Default submission status is now set to _Not Attempted_.
- Renamed `Python` to `Python3`.
- `marks` field in **Question** model is now `NULL` acceptable.


## [1.0.0] - Nov 27, 2019
- Initial Release