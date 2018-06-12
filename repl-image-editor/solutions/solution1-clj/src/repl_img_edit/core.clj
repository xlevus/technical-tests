(ns repl-img-edit.core
  (:require [clojure.string :refer [split join]]
            [clojure.main :refer [repl]]))

(def default-colour "O")


(defn dimensions
  "Get the dimensions of an image"
  [image]
  [(count (first image)) (count image)])


(defn get-pixel [img x y]
  (get-in img [y x]))

(defn spy-pixel [img x y]
  (println x "x" y " = " (get-pixel img x y))
  img)


(defn spy-img [img]
  (println img)
  img)

(defn new-image
  "Create a new 'image' with dimensions w*h"
  [w h]
  (->> default-colour
       repeat
       (take w)
       vec
       repeat
       (take h)
       vec))


(defn clear-image
  "Return a new image, with all pixels set to the default colour."
  [img]
  (apply new-image (dimensions img)))


(defn set-pixel [img x y c]
  (assoc-in img [y x] c))


(defn draw-vertical [img x y1 y2 c]
  (reduce #(set-pixel %1 x %2 c) img (range y1 (inc y2))))


(defn draw-horizontal [img x1 x2 y c]
  (reduce #(set-pixel %1 %2 y c) img (range x1 (inc x2))))


(defn fill
  ([img x y c] (fill img x y c (get-pixel img x y)))
  ([img x y c t]
   (if (= (get-pixel img x y) t)
     (-> img
         (set-pixel x y c)
         ;; Stack depth issues ahoy?
         (fill (inc x) y c t)
         (fill (dec x) y c t)
         (fill x (inc y) c t)
         (fill x (dec y) c t)
         )
     img)))

(defn format-img [img]
  (join "\n" (map join img)))


(defn colour [c] c)
(defn coordinate [c] (Integer/parseInt c))


(defn main- []
  (println "Just use the clojure repl."))
