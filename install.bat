echo "============================="
echo "+++++++ Test 1: +++++++++++++"
echo "============================="
echo "Check that NodeJS is installed:"
node --version
echo ""

echo "============================="
echo "+++++++ Test 2: +++++++++++++"
echo "============================="
echo "Check that Python3 is installed:"
python --version
echo ""

echo "============================="
echo "+++++++ Test 3: +++++++++++++"
echo "============================="
echo "Check that Pip is installed:"
pip --version
echo ""

echo "============================="
echo "+++++++ Test 4: +++++++++++++"
echo "============================="
echo "Check that npm is installed:"
npm --version
echo ""

echo "================================================"
echo "+++++++ Installing NodeJS modules: +++++++++++++"
echo "================================================"
echo "cd webpage"
cd webpage
echo "npm install"
npm install
echo "cd .."
cd ..
echo ""

echo "====================================="
echo "++++ Installing Python Modules: +++++"
echo "====================================="
echo ""

echo "pip install numpy"
pip install numpy
echo ""

echo "pip install -U scikit-learn"
pip3 install scikit-learn
echo ""

echo "pip install opencv-python"
pip3 install opencv-python
echo ""

echo "pip install -U scikit-image"
pip3 install scikit-image --user
echo ""



