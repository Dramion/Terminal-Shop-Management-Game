"""Program initializer"""

if __name__ == "__main__":
    import src.scripts.classes as classPy
    store = classPy.Store(
        input("What would you like the name of your store to be?"), 30)

    print(store)
