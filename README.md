<h1 align="center">CodeClassroom API</h1>
<p align="center">
  <img alt="CodeClassroom Logo" src="https://avatars1.githubusercontent.com/u/51260271?s=200&v=4" />
</p>



[![Build Status](https://travis-ci.org/codeclassroom/codeclassroom.svg?branch=master)](https://travis-ci.org/codeclassroom/codeclassroom)
![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/codeclassroom/codeclassroom)
[![Requirements Status](https://requires.io/github/codeclassroom/codeclassroom/requirements.svg?branch=master)](https://requires.io/github/codeclassroom/codeclassroom/requirements/?branch=master)
[![CodeFactor](https://www.codefactor.io/repository/github/codeclassroom/codeclassroom/badge)](https://www.codefactor.io/repository/github/codeclassroom/codeclassroom)  
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/91c4c80af77442d5979eb5253afa3759)](https://www.codacy.com/gh/codeclassroom/codeclassroom?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=codeclassroom/codeclassroom&amp;utm_campaign=Badge_Grade)
[![Maintainability](https://api.codeclimate.com/v1/badges/982b856aa598f852f9a8/maintainability)](https://codeclimate.com/github/codeclassroom/codeclassroom/maintainability)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/codeclassroom/codeclassroom.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/codeclassroom/codeclassroom/alerts/)
[![GitHub](https://img.shields.io/github/license/codeclassroom/codeclassroom)](https://github.com/codeclassroom/codeclassroom/blob/master/LICENSE)

## Developing 👷

#### Prerequisties
- Python 3.6.8+
- virtualenv

1. Create Virtual Environment.
```bash
virtualenv -p python3 cc && cd cc && source bin/activate
```
2. Clone repository.
```bash
git clone https://github.com/codeclassroom/codeclassroom.git
```
3. Install Dependencies.
```bash
pip3 install -r requirements.txt
```
4. Migrate Changes.
```bash
python3 manage.py migrate
```
5. Run tests.
```bash
python3 manage.py test
```
6. Run Server
```bash
python3 manage.py runserver
```

## Change log 📝

Changelog can be found in [Releases](https://github.com/codeclassroom/codeclassroom/releases).

## Authors 🔮

👥 **Bhupesh Varshney**

- Twitter: [@bhupeshimself](https://twitter.com/bhupeshimself)
- DEV: [bhupesh](https://dev.to/bhupesh)

👥 **Gagan Singh**

- GitHub: [GAGANsinghmsitece](https://github.com/GAGANsinghmsitece)

👥 **Animesh Ghosh**

- GitHub: [Animesh-Ghosh](https://github.com/Animesh-Ghosh)


## License 📜

This project is licensed under the AGPL-3.0 License. See the [LICENSE](LICENSE) file for details.

## Contributing 🍰

Please read [CONTRIBUTING](CONTRIBUTING.md) for details on our [CODE OF CONDUCT](CODE_OF_CONDUCT.md), and the process for submitting pull requests to us.
