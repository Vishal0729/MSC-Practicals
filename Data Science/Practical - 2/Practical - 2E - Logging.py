import os, logging, uuid, shutil, time

Base = r"D:/MSC Practicals/Data Science/Practical - 2/Outputs/Practical - 2E/"
Companies = ['01-Vermeulen', '02-Krennwallner', '03-Hillman', '04-Clark']
Layers = ['01-Retrieve','02-Assess','03-Process','04-Transform','05-Organise','06-Report']
Levels = ['debug','info','warning','error']

for comp in Companies:
    for layer in Layers:
        log_dir = os.path.join(Base, comp, layer, "Logging")
        if os.path.exists(log_dir):
            shutil.rmtree(log_dir)
            time.sleep(1)
        os.makedirs(log_dir)

        log_file = os.path.join(log_dir, f"Logging_{uuid.uuid4()}.log")
        print("Creating log file:", log_file)

        # Reset logging to avoid repeated console output
        for h in logging.root.handlers[:]:
            logging.root.removeHandler(h)

        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)-8s %(message)s',
            filename=log_file,
            filemode='w'
        )

        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        logging.getLogger('').addHandler(console)

        logging.info("Practical Data Science is fun!")

        # Log messages for each level
        for lvl in Levels:
            getattr(logging, lvl)(f"{lvl.capitalize()} message recorded.")

print("/n Done! All folders and logs created successfully.")

