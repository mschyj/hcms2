python setup.py install
cd pythonsdk
pip install -r requirements.txt
python setup.py install
export PYTHONPATH=.:/usr/local/lib/python2.7/site-packages/openstack
cd ..
echo "|======================================================================|"
echo " Installation is completed "
echo " Please run the script Inithwcc.sh to setup your environment "     
echo "|======================================================================|"

