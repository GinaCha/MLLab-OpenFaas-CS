from imageai.Detection import ObjectDetection
import os
import json
from urllib import request

def handle(req):
    """
       Perform object detection. The models supported are
       RetinaNet, YOLOv3 and TinyYOLOv3. This means you can
       detect and recognize 80 different kind of common
       everyday objects.

        Parameters
        ----------
        str : String
            the provided url of the image
            - model (required) available values retina, yolo and yolo-tiny
            - detection_speed (optional) available values “normal”, “fast”, “faster”, “fastest” and “flash”
            - input_image (required) path to image file which you want to detect. You can set this parameter to
                 the Numpy array of File stream of any image if you set the paramter input_type to “array” or “stream”
            - input_type (hiden) available values “array”, “stream”, “file”
            - output_image_path (required only if input_type = “file” ) refers to the file path to which the detected image
                will be saved.
            - minimum_percentage_probability (optional ) : This parameter is used to determine the integrity of the detection
                results. Lowering the value shows more objects while increasing the value ensures objects with the highest
                accuracy are detected. The default value is 50.
            - output_type (optional ) : This parameter is used to set the format in which the detected image will be produced.
                The available values are “file” and “array”. The default value is “file”. If this parameter is set to “array”,
                the function will return a Numpy array of the detected image
            - display_percentage_probability (optional ) : This parameter can be used to hide the percentage probability of each
                 object detected in the detected image if set to False. The default values is True.
            - display_object_name (optional ) : This parameter can be used to hide the name of each object detected in the
                detected image if set to False. The default values is True.
            - extract_detected_objects (optional ) : This parameter can be used to extract and save/return each object detected
                in an image as a seperate image. The default values is False.
            - thread_safe (optional) : This ensures the loaded detection model works across all threads if set to true.
            - custom_objects (optional ) : include a array with the object names available tags are :  person,   bicycle,
                 car,   motorcycle,   airplane, bus,   train,   truck,   boat,   traffic light,   fire hydrant,   stop_sign,
                parking meter,   bench,   bird,   cat,   dog,   horse,   sheep,   cow,   elephant,   bear,   zebra,
                giraffe,   backpack,   umbrella,   handbag,   tie,   suitcase,   frisbee,   skis,   snowboard,
                sports ball,   kite,   baseball bat,   baseball glove,   skateboard,   surfboard,   tennis racket,
                bottle,   wine glass,   cup,   fork,   knife,   spoon,   bowl,   banana,   apple,   sandwich,   orange,
                broccoli,   carrot,   hot dog,   pizza,   donot,   cake,   chair,   couch,   potted plant,   bed,
                dining table,   toilet,   tv,   laptop,   mouse,   remote,   keyboard,   cell phone,   microwave,
                oven,   toaster,   sink,   refrigerator,   book,   clock,   vase,   scissors,   teddy bear,   hair dryer,
                toothbrush.
        Returns
        -------
        str
           depend on the parameters parsed into.
    """

    parameters = json.loads(req)
    execution_path = os.getcwd()
    data = request.urlopen(parameters["url"])

    detection_speed = "normal"
    if "detection_speed" in parameters:
        detection_speed = parameters["detection_speed"]

    minimum_percentage_probability = 50
    if "minimum_percentage_probability" in parameters:
        minimum_percentage_probability = parameters["minimum_percentage_probability"]

    extracted_objects = False
    if "extracted_objects" in parameters:
        extracted_objects = parameters["extracted_objects"]

    display_object_name = True
    if "display_object_name" in parameters:
        display_object_name = parameters["display_object_name"]

    display_percentage_probability  = True
    if "display_percentage_probability" in parameters:
        display_percentage_probability = parameters["display_percentage_probability"]

    thread_safe = False
    if "thread_safe" in parameters:
        thread_safe = parameters["thread_safe"]

    detector = ObjectDetection()
    if (len(parameters['model']) > 0):
        if (parameters['model']  == "retina"):
                detector.setModelTypeAsRetinaNet() #sets the model type of the object detection instance to the RetinaNet model
                detector.setModelPath( os.path.join(execution_path , "resnet50_coco_best_v2.1.0.h5"))# the path to the model file you downloaded and must corresponds to the model type you set for the object detection instance.
        elif (parameters['model']  == "yolo"):
                detector.setModelTypeAsYOLOv3() #sets the model type of the object detection instance to the YOLOv3 model
                detector.setModelPath( os.path.join(execution_path , "yolo.h5"))# the path to the model file you downloaded and must corresponds to the model type you set for the object detection instance.
        elif (parameters['model']  == "yolo-tiny"):
                detector.setModelTypeAsTinyYOLOv3() #sets the model type of the object detection instance to the TinyYOLOv3 model
                detector.setModelPath( os.path.join(execution_path , "yolo-tiny.h5"))# the path to the model file you downloaded and must corresponds to the model type you set for the object detection instance.

        detector.loadModel()
        if ( "custom_objects" in parameters and len(parameters["custom_objects"]) == 0 ):
            if (parameters["output_type"] == "file" and extracted_objects == False):
                detections = detector.detectObjectsFromImage(
                                                            input_image=data,
                                                            input_type="array",
                                                            output_image_path=os.path.join(execution_path , "imagenew.jpg"),
                                                            detection_speed=detection_speed,
                                                            display_object_name=display_object_name,
                                                            thread_safe=thread_safe,
                                                            display_percentage_probability=display_percentage_probability ,
                                                            minimum_percentage_probability=minimum_percentage_probability)
                print( json.dumps({"detections" : detections}) )

            elif (parameters["output_type"] == "array" and extracted_objects == False):
                returned_image, detections = detector.detectObjectsFromImage(input_image=data,
                                                            input_type="array",
                                                            output_type="array",
                                                            detection_speed=detection_speed,
                                                            display_object_name=display_object_name,
                                                            thread_safe=thread_safe,
                                                            display_percentage_probability=display_percentage_probability ,
                                                            minimum_percentage_probability=minimum_percentage_probability)
                print( json.dumps({"detections" : detections, "image": returned_image}) )

            elif (parameters["output_type"] == "file" and extracted_objects == True):
                detections, extracted_objects = detector.detectObjectsFromImage(
                                                            input_image=data,
                                                            input_type="array",
                                                            output_image_path=os.path.join(execution_path , "imagenew.jpg"),
                                                            extract_detected_objects=True,
                                                            detection_speed=detection_speed,
                                                            display_object_name=display_object_name,
                                                            thread_safe=thread_safe,
                                                            display_percentage_probability=display_percentage_probability ,
                                                            minimum_percentage_probability=minimum_percentage_probability)
                print( json.dumps({"detections" : detections, "extracted_objects": extracted_objects}) )

            elif (parameters["output_type"] == "array" and extracted_objects == False):
                returned_image, detections, extracted_objects = detector.detectObjectsFromImage(
                                                            input_image=data,
                                                            input_type="array",
                                                            output_type="array",
                                                            extract_detected_objects=True,
                                                            detection_speed=detection_speed,
                                                            display_object_name=display_object_name,
                                                            thread_safe=thread_safe,
                                                            display_percentage_probability=display_percentage_probability ,
                                                            minimum_percentage_probability=minimum_percentage_probability)
                print( json.dumps({"detections" : detections, "image": returned_image, "extracted_objects": extracted_objects}) )


        #################### CUSTOM OBJECT DETECTION

        else: 
            person = False
            if "person" in parameters["extracted_objects"]:
                person=True

            bicycle = False
            if "bicycle" in parameters["extracted_objects"]:
                bicycle=True
                
            car = False
            if "car" in parameters["extracted_objects"]:
                car=True
                
            motorcycle = False
            if "motorcycle" in parameters["extracted_objects"]:
                motorcycle=True
                
            airplane = False
            if "airplane" in parameters["extracted_objects"]:
                airplane=True
                
            bus = False
            if "bus" in parameters["extracted_objects"]:
                bus=True
                
            train = False
            if "train" in parameters["extracted_objects"]:
                train=True
                
            truck = False
            if "truck" in parameters["extracted_objects"]:
                truck=True
                
            boat = False
            if "boat" in parameters["extracted_objects"]:
                boat=True
                
            traffic_light = False
            if "traffic_light" in parameters["extracted_objects"]:
                traffic_light=True
                
            fire_hydrant = False
            if "fire_hydrant" in parameters["extracted_objects"]:
                fire_hydrant=True
                
            stop_sign = False
            if "stop_sign" in parameters["extracted_objects"]:
                stop_sign=True
                
            parking_meter = False
            if "parking_meter" in parameters["extracted_objects"]:
                parking_meter=True
                
            bench = False
            if "bench" in parameters["extracted_objects"]:
                bench=True
                
            bird = False
            if "bird" in parameters["extracted_objects"]:
                bird=True
                
            cat = False
            if "cat" in parameters["extracted_objects"]:
                cat=True
                
            dog = False
            if "dog" in parameters["extracted_objects"]:
                dog=True
                
            horse = False
            if "person" in parameters["extracted_objects"]:
                person=True
                
            sheep = False
            if "sheep" in parameters["extracted_objects"]:
                sheep=True
                
            cow = False
            if "cow" in parameters["extracted_objects"]:
                cow=True
                
            elephant = False
            if "elephant" in parameters["extracted_objects"]:
                elephant=True
                
            bear = False
            if "bear" in parameters["extracted_objects"]:
                bear=True
                
            zebra = False
            if "zebra" in parameters["extracted_objects"]:
                zebra=True
                
            giraffe = False
            if "giraffe" in parameters["extracted_objects"]:
                giraffe=True
                
            backpack = False
            if "backpack" in parameters["extracted_objects"]:
                backpack=True
                
            umbrella = False
            if "umbrella" in parameters["extracted_objects"]:
                umbrella=True
                
            handbag = False
            if "handbag" in parameters["extracted_objects"]:
                handbag=True
                
            tie = False
            if "tie" in parameters["extracted_objects"]:
                tie=True
                
            suitcase = False
            if "suitcase" in parameters["extracted_objects"]:
                suitcase=True
                
            frisbee = False
            if "frisbee" in parameters["extracted_objects"]:
                frisbee=True
                
            skis = False
            if "skis" in parameters["extracted_objects"]:
                skis=True
                
            snowboard = False
            if "snowboard" in parameters["extracted_objects"]:
                snowboard=True
                
            sports_ball = False
            if "sports_ball" in parameters["extracted_objects"]:
                sports_ball=True
                
            kite = False
            if "kite" in parameters["extracted_objects"]:
                kite=True
                
            baseball_bat = False
            if "person" in parameters["extracted_objects"]:
                person=True
                
            baseball_glove = False
            if "baseball_glove" in parameters["extracted_objects"]:
                baseball_glove=True
                
            skateboard = False
            if "skateboard" in parameters["extracted_objects"]:
                skateboard=True
                
            surfboard = False
            if "surfboard" in parameters["extracted_objects"]:
                surfboard=True
                
            tennis_racket = False
            if "tennis_racket" in parameters["extracted_objects"]:
                tennis_racket=True
                
            bottle = False
            if "bottle" in parameters["extracted_objects"]:
                bottle=True
                
            wine_glass = False
            if "wine_glass" in parameters["extracted_objects"]:
                wine_glass=True
                
            cup = False
            if "cup" in parameters["extracted_objects"]:
                cup=True
                
            fork = False
            if "fork" in parameters["extracted_objects"]:
                fork=True
                
            knife = False
            if "knife" in parameters["extracted_objects"]:
                knife=True
                
            spoon = False
            if "spoon" in parameters["extracted_objects"]:
                spoon=True
                
            bowl = False
            if "bowl" in parameters["extracted_objects"]:
                bowl=True
                
            banana = False
            if "banana" in parameters["extracted_objects"]:
                banana=True
                
            apple = False
            if "apple" in parameters["extracted_objects"]:
                apple=True
                
            sandwich = False
            if "sandwich" in parameters["extracted_objects"]:
                sandwich=True
                
            orange = False
            if "orange" in parameters["extracted_objects"]:
                orange=True
                
            broccoli = False
            if "broccoli" in parameters["extracted_objects"]:
                broccoli=True
                
            carrot = False
            if "carrot" in parameters["extracted_objects"]:
                carrot=True
                
            hot_dog = False
            if "hot_dog" in parameters["extracted_objects"]:
                hot_dog=True
                
            pizza = False
            if "pizza" in parameters["extracted_objects"]:
                pizza=True
                
            donot = False
            if "donot" in parameters["extracted_objects"]:
                donot=True
                
            cake = False
            if "cake" in parameters["extracted_objects"]:
                cake=True
                
            chair = False
            if "chair" in parameters["extracted_objects"]:
                chair=True
                
            couch = False
            if "couch" in parameters["extracted_objects"]:
                couch=True
                
            potted_plant = False
            if "potted_plant" in parameters["extracted_objects"]:
                potted_plant=True
                
            bed = False
            if "bed" in parameters["extracted_objects"]:
                bed=True
                
            dining_table = False
            if "dining_table" in parameters["extracted_objects"]:
                dining_table=True
                
            toilet = False
            if "toilet" in parameters["extracted_objects"]:
                toilet=True
                
            tv = False
            if "tv" in parameters["extracted_objects"]:
                tv=True
                
            laptop = False
            if "laptop" in parameters["extracted_objects"]:
                laptop=True
                
            mouse = False
            if "mouse" in parameters["extracted_objects"]:
                mouse=True
                
            remote = False
            if "remote" in parameters["extracted_objects"]:
                remote=True
                
            keyboard = False
            if "keyboard" in parameters["extracted_objects"]:
                keyboard=True
                
            cell_phone = False
            if "cell_phone" in parameters["extracted_objects"]:
                cell_phone=True
                
            microwave = False
            if "microwave" in parameters["extracted_objects"]:
                microwave=True
                
            oven = False
            if "oven" in parameters["extracted_objects"]:
                oven=True
                
            toaster = False
            if "toaster" in parameters["extracted_objects"]:
                toaster=True
                
            sink = False
            if "sink" in parameters["extracted_objects"]:
                sink=True
                
            refrigerator = False
            if "refrigerator" in parameters["extracted_objects"]:
                refrigerator=True
                
            book = False
            if "book" in parameters["extracted_objects"]:
                book=True
                
            clock = False
            if "clock" in parameters["extracted_objects"]:
                clock=True
                
            vase = False
            if "vase" in parameters["extracted_objects"]:
                vase=True
                
            scissors = False
            if "scissors" in parameters["extracted_objects"]:
                scissors=True
                
            teddy_bear = False
            if "teddy_bear" in parameters["extracted_objects"]:
                teddy_bear=True
                
            hair_dryer = False
            if "hair_dryer" in parameters["extracted_objects"]:
                hair_dryer=True
                
            toothbrush = False
            if "toothbrush" in parameters["extracted_objects"]:
                toothbrush=True
            

            custom =  detector.CustomObjects(
                                            person=person,
                                            bicycle=bicycle,
                                            car=car,
                                            motorcycle=motorcycle,
                                            airplane=airplane,
                                            bus=bus,
                                            train=train,
                                            truck=truck,
                                            boat=boat,
                                            traffic_light=traffic_light,
                                            fire_hydrant=fire_hydrant,
                                            stop_sign=stop_sign,
                                            parking_meter=parking_meter,
                                            bench=bench,
                                            bird=bird,
                                            cat=cat,
                                            dog=dog,
                                            horse=horse,
                                            sheep=sheep,
                                            cow=cow,
                                            elephant=elephant,
                                            bear=bear,
                                            zebra=zebra,
                                            giraffe=giraffe,
                                            backpack=backpack,
                                            umbrella=umbrella,
                                            handbag=handbag,
                                            tie=tie,
                                            suitcase=suitcase,
                                            frisbee=frisbee,
                                            skis=skis,
                                            snowboard=snowboard,
                                            sports_ball=sports_ball,
                                            kite=kite,
                                            baseball_bat=baseball_bat,
                                            baseball_glove=baseball_glove,
                                            skateboard=skateboard,
                                            surfboard=surfboard,
                                            tennis_racket=tennis_racket,
                                            bottle=bottle,
                                            wine_glass=wine_glass,
                                            cup=cup,
                                            fork=fork,
                                            knife=knife,
                                            spoon=spoon,
                                            bowl=bowl,
                                            banana=banana,
                                            apple=apple,
                                            sandwich=sandwich,
                                            orange=orange,
                                            broccoli=broccoli,
                                            carrot=carrot,
                                            hot_dog=hot_dog,
                                            pizza=pizza,
                                            donot=donot,
                                            cake=cake,
                                            chair=chair,
                                            couch=couch,
                                            potted_plant=potted_plant,
                                            bed=bed,
                                            dining_table=dining_table,
                                            toilet=toilet,
                                            tv=tv,
                                            laptop=laptop,
                                            mouse=mouse,
                                            remote=remote,
                                            keyboard=keyboard,
                                            cell_phone=cell_phone,
                                            microwave=microwave,
                                            oven=oven,
                                            toaster=toaster,
                                            sink=sink,
                                            refrigerator=refrigerator,
                                            book=book,
                                            clock=clock,
                                            vase=vase,
                                            scissors=scissors,
                                            teddy_bear=teddy_bear,
                                            hair_dryer=hair_dryer,
                                            toothbrush=toothbrush
                                        )



            if (parameters["output_type"] == "file" and extracted_objects == False):
                detections = detector.detectCustomObjectsFromImage(
                                                            custom_objects=custom,
                                                            input_image=data,
                                                            input_type="array",
                                                            output_image_path=os.path.join(execution_path , "imagenew.jpg"),
                                                            detection_speed=detection_speed,
                                                            display_object_name=display_object_name,
                                                            thread_safe=thread_safe,
                                                            display_percentage_probability=display_percentage_probability,
                                                            minimum_percentage_probability=minimum_percentage_probability)
                print( json.dumps({"detections" : detections}) )

            elif (parameters["output_type"] == "array" and extracted_objects == False):
                returned_image, detections = detector.detectCustomObjectsFromImage(input_image=data,
                                                            custom_objects=custom,
                                                            input_type="array",
                                                            output_type="array",
                                                            detection_speed=detection_speed,
                                                            display_object_name=display_object_name,
                                                            thread_safe=thread_safe,
                                                            display_percentage_probability=display_percentage_probability ,
                                                            minimum_percentage_probability=minimum_percentage_probability)
                print( json.dumps({"detections" : detections, "image": returned_image}) )

            elif (parameters["output_type"] == "file" and extracted_objects == True):
                detections, extracted_objects = detector.detectCustomObjectsFromImage(
                                                            custom_objects=custom,
                                                            input_image=data,
                                                            input_type="array",
                                                            output_image_path=os.path.join(execution_path , "imagenew.jpg"),
                                                            extract_detected_objects=True,
                                                            detection_speed=detection_speed,
                                                            display_object_name=display_object_name,
                                                            thread_safe=thread_safe,
                                                            display_percentage_probability=display_percentage_probability,
                                                            minimum_percentage_probability=minimum_percentage_probability)
                print( json.dumps({"detections" : detections, "extracted_objects": extracted_objects}) )

            elif (parameters["output_type"] == "array" and extracted_objects == True):
                returned_image, detections, extracted_objects = detector.detectCustomObjectsFromImage(input_image=data,
                                                            custom_objects=custom,
                                                            input_type="array",
                                                            output_type="array",
                                                            extract_detected_objects=True,
                                                            detection_speed=detection_speed,
                                                            display_object_name=display_object_name,
                                                            thread_safe=thread_safe,
                                                            display_percentage_probability=display_percentage_probability ,
                                                            minimum_percentage_probability=minimum_percentage_probability)
                print( json.dumps({"detections" : detections, "image": returned_image, "extracted_objects": extracted_objects}) )


    else:
        print("*** Need to select a model first.")

