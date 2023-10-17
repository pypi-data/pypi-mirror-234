from setuptools import setup, find_packages
   
setup(
        name= 'DCU_gibic',
        version='0.1', 
        long_description_content_type='text/markdown',
        description='use EASY lib supporting DCU gibic lecture',
        author='applenongbu',
        author_email= 'hutk1726@naver.com', 
        url='https://github.com/applenongbu/DCU_gibic', # github url
        download_url        = 'https://github.com/applenongbu/DCU_gibic/archive/master.zip', # release 이름
        install_requires    =  ["pandas"], # 패키지 사용시 필요한 모듈
        packages            = find_packages(exclude = []),
        keywords            = ['gibic', 'dcu'], # 키워드
        python_requires     = '>=3.6', # python 필요 버전
        package_data        = {}, 
        zip_safe            = False,
        classifiers         = [   
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7'
            
        ],
    )
