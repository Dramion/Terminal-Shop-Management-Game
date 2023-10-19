"""Program initializer"""
import src.scripts.functions as funcPy

if __name__ == "__main__":
    store = funcPy.start()
    for i in range(10):
        store.customers.append(funcPy.new_customer())
    print(store)
