## GohlkeBrowser

<pre>
me@DESKTOP D:\Project\Python\GohlkeBrowser
$ python gohlke_browser.py
Welcome to the GohlkeBrowser.
Type help or ? to list commands.

[cp2.7.10-amd64@/]>> search numpy cp27
  1598: netCDF4-1.1.7+numpy16-cp27-none-win32.whl
  1599: netCDF4-1.1.7+numpy16-cp27-none-win_amd64.whl
  1658: numpy-1.11.2+mkl-cp27-cp27m-win32.whl
  1659: numpy-1.11.2+mkl-cp27-cp27m-win_amd64.whl
  2642: vigranumpy-1.10.0-cp27-cp27m-win32.whl
  2643: vigranumpy-1.10.0-cp27-cp27m-win_amd64.whl
[cp2.7.10-amd64@/]>> download 1659 d:\somepath
Total 28072658 bytes -> 16% .. 32% .. 48% .. 64% .. 80% .. 96% .. 100%%
d:\somepath\numpy-1.11.2+mkl-cp27-cp27m-win_amd64.whl ... done
[cp2.7.10-amd64@/]>> install 1659
Total 28072658 bytes -> 16% .. 32% .. 48% .. 64% .. 80% .. 96% .. 100%%
Processing c:\users\me\appdata\local\temp\numpy-1.11.2+mkl-cp27-cp27m-win_amd64.whl
Installing collected packages: numpy
 Found existing installation: numpy 1.11.2
    Uninstalling numpy-1.11.2:
      Successfully uninstalled numpy-1.11.2
Successfully installed numpy-1.11.2+mkl
[cp2.7.10-amd64@/]>> bye
</pre>