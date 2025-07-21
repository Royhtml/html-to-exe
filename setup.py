from setuptools import setup, find_packages
import os

# Baca README dengan encoding UTF-8
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md'), 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="html-to-exe",
    version="1.0.0",
    author="Dwi Bakti N Dev",
    author_email="dwibakti76@gmail.com",
    description="Konversi HTML ke EXE berbasis Electron",
    long_description=long_description,  # Gunakan variabel yang sudah dibaca
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pillow>=8.0",
        "pyinstaller>=4.0",
        "pyqt5>=5.15",
    ],
    entry_points={
        "gui_scripts": [
            "html-to-exe=html_to_exe.cli:main",
        ],
    },
    include_package_data=True,
    package_data={
        "html_to_exe": ["*.ico", "*.png"],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
print("Isi README:", long_description[:100])  # Cetak 100 karakter pertama