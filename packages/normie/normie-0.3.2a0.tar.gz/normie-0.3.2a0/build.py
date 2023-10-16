from setuptools import Extension


# define the extension module
src_dir = "src/"
normie_impl = Extension(
    'normie_impl',
    sources=[
        src_dir + 'normie_impl.c',
    ],
    include_dirs=[src_dir]
)


def build(setup_kwargs):
    setup_kwargs.update(
        {
            "ext_modules": [normie_impl],
        }
    )
