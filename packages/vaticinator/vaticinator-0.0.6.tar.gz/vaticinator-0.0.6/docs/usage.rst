Usage
=====

It's pretty simple.

To use ``vaticinator``::

    import vaticinator

or::

    from vaticinator import Vaticinator
    vat = Vaticinator()
    vat.process_options(
        'long', 'debug', 
        'off', short_max=100
    )
    print(vat.fortune)

or on the command line::

    alias fortune=vaticinator
    fortune -sov

Still stuck?  Try::

    vaticinator --help
