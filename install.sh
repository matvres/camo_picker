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
python3 --version
echo ""

echo "============================="
echo "+++++++ Test 3: +++++++++++++"
echo "============================="
echo "Check that Pip3 is installed:"
pip3 --version
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

echo "pip3 install -U scikit-learn"
pip3 install -U scikit-learn
echo ""

echo "pip install opencv-python"
pip install opencv-python
echo ""

echo "pip install -U scikit-image"
pip install -U scikit-image
echo ""


