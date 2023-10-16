from setuptools import setup, find_packages


def requirements():
	requirements_list = list()
	with open('requirements.txt') as pc_requirements:
		for install in pc_requirements:
			requirements_list.append(
				install.strip()
			)
	return requirements_list


with open("README.md", "r", encoding="utf-8") as desc_long:
	description_long = desc_long.read()


setup(
	name='aiosmshub',
	version='0.0.1',
	description='Asynchronous module for working with the SMSHub API',
	long_description=description_long,
	packages=find_packages(),
	long_description_content_type='text/markdown',
	author='VoXDoX',
	author_email='1voxdox1@gmail.com',
	keywords=['smshub', 'smshub api', 'api smshub'],
	zip_safe=False,
	install_requires=requirements(),
	project_urls={
		"TG Channel": "https://t.me/AsyncModules",
		"Github": "https://github.com/VoXDoX/aiosmshub",
	},
	python_requires=">=3.7"
)
