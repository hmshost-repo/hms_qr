mkdir -p src/{pages/{sim1,sim2},locators,utils,data} tests
mkdir -p reports/{html,screenshots}
mkdir -p logs/{store_logs,test_runs}

touch src/pages/{base_page.py,__init__.py}
touch src/pages/sim1/{__init__.py,menu_page.py,cart_page.py,checkout_page.py}
touch src/pages/sim2/{__init__.py,menu_page.py,cart_page.py,checkout_page.py}
touch src/locators/{__init__.py,sim1_locators.py,sim2_locators.py}
touch src/utils/{__init__.py,driver_factory.py,config_reader.py,logger.py}
touch src/data/{sim1_stores.csv,sim2_stores.csv}
touch tests/{__init__.py,test_checkout.py,test_price_check.py}
touch {conftest.py,pytest.ini,pyproject.toml,requirements.txt,README.md}

touch reports/html/.gitkeep
touch reports/screenshots/.gitkeep
touch logs/store_logs/.gitkeep
touch logs/test_runs/.gitkeep 