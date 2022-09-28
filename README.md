# pyDash: A Framework Based Educational Tool for Adaptive Streaming Video Algorithms Study

![bigbuckbunny](https://user-images.githubusercontent.com/4336448/118493151-2b9fc380-b6f7-11eb-8a25-9134862da754.jpg) A Python Dash Project. 

PyDash is a framework for the development of adaptive streaming video algorithms. It is a learning tool designed to abstract the networking communication details, allowing e-students to focus exclusively on developing and evaluating ABR protocols.

PyDash is licensed as GPL. You are more than welcome to use PyDash and contribute to the project. We just ask you to properly cite our contribution as follows.

> M. A. Marotta, G. C. Souza, M. Holanda and M. F. Caetano, ["PyDash - A Framework Based Educational Tool for Adaptive Streaming Video Algorithms Study"](https://ieeexplore.ieee.org/document/9637335), 2021 IEEE Frontiers in Education Conference (FIE), 2021, pp. 1-8, doi: 10.1109/FIE49875.2021.9637335.


# Who we are?

We are from the **Department of Computer Science** at the **University of Brasília (UnB)**, Brazil.

This project is leaded by [Prof. Dr. Marcos Caetano](mailto:mfcaetano@unb.br) and [Prof. Dr. Marcelo Marotta](mailto:marcelo.marotta@unb.br). 

If you have any questions regarding the pyDash project, please drop us an email.


# Instalation Process

## Requirements

It is necessary the installation of few python packages before you can use PyDash. The requirements are described in [requirements.txt](requirements.txt) file. 

## Where do I start?

There are a few ways for you to set your development environment. In this section, we will present you with just one possible way to do this.

* The first step is to do the checkout of the pyDash source code. You should have git software installed on your operating system. Using a terminal, do the pyDash source code repository clone operation.

```
git clone https://github.com/mfcaetano/pydash.git
```

If you are doing a Computer Networking class at the Department of Computer Science at the UnB, we strongly suggest that you should clone the repository instead of just downloading it. Source code updates could be available and new functionalities released during the current semester.

```
python3 -m venv pydash/venv
```

* Get in the repository folder.

```
cd pydash
```

* The next step is to activate the terminal and load the python configurations.

```
source venv/bin/activate
```

* Now, you need to install the dependency libraries used by pyDash.
```
pip3 install -r requirements.txt
```

Done! To test your pyDash installation, you have to execute:
```
python3 main.py
```

# Architecture 

![Arquitetura](https://user-images.githubusercontent.com/4336448/98450304-85a54800-211a-11eb-93f7-fd4e60c46ed5.png)

![Arquitetura_Servidor](https://user-images.githubusercontent.com/4336448/98450354-ea60a280-211a-11eb-9fd9-1f7e1ddc1f9c.png)

![Arquitetura_Cliente](https://user-images.githubusercontent.com/4336448/98450355-ec2a6600-211a-11eb-9845-298b51f9801e.png)



