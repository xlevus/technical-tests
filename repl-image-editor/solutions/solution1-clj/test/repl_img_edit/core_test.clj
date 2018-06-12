(ns repl-img-edit.core-test
  (:require [clojure.test :refer :all]
            [repl-img-edit.core :refer :all]))


(deftest test-dimensions
  (is (= [3 2]
         (dimensions (new-image 3 2)))))


(deftest test-get-pixel
  (let [img [["0x0" "1x0"]
             ["0x1" "1x1"]]]
    (testing "Within Bounds"
      (is (= "0x0" (get-pixel img 0 0)))
      (is (= "0x1" (get-pixel img 0 1)))
      (is (= "1x0" (get-pixel img 1 0)))
      (is (= "1x1" (get-pixel img 1 1))))

    (testing "Out of bounds"
      (is (= nil (get-pixel img 2 0))))))


(deftest new-image-test
  (testing "single pixel"
    (is (= [["O"]]
           (new-image 1 1))))

  (testing "create buffer"
    (is (= [["O" "O" "O"]
            ["O" "O" "O"]]
           (new-image 3 2)))))


(deftest clear-image-test
  (testing "clear"
    (is (= (new-image 3 1)
           (clear-image [["A" "B" "C"]])))))

(deftest set-pixel-test
  (testing "single pixel"
    (is (= [["X"]]
           (-> (new-image 1 1)
               (set-pixel 0 0 "X")))))

  (testing "more pixels"
    (is (= [["O" "O" "O" "O"]
            ["O" "X" "O" "O"]
            ["O" "O" "O" "O"]]
           (-> (new-image 4 3)
               (set-pixel 1 1 "X"))))

    (is (= [["O" "X" "O" "O"]
            ["O" "O" "O" "O"]
            ["O" "O" "O" "O"]]
           (-> (new-image 4 3)
               (set-pixel 1 0 "X"))))

    (is (= [["O" "O" "O" "O"]
            ["O" "O" "O" "O"]
            ["O" "O" "O" "X"]]
           (-> (new-image 4 3)
               (set-pixel 3 2 "X")))) 
    ))


(deftest draw-vertical-test
  (is (= [["O" "O" "O"]
          ["O" "X" "O"]
          ["O" "X" "O"]
          ["O" "O" "O"]]
         (-> (new-image 3 4)
             (draw-vertical 1 1 2 "X")))))


(deftest draw-horizontal-test
  (is (= [["O" "O" "O" "O"]
          ["O" "O" "O" "O"]
          ["O" "X" "X" "O"]
          ["O" "O" "O" "O"]]
         (-> (new-image 4 4)
             (draw-horizontal 1 2 2 "X")))))


(deftest fill-test
  (testing "simple fill"
    (is (= [["X" "X" "X"]
            ["X" "X" "X"]
            ["X" "X" "X"]]
           (-> (new-image 3 3)
               (fill 1 1 "X")))))

  (testing "complex fill"
    (is (= [["T" "O" "O" "O" "O"]
            ["O" "X" "X" "X" "O"]
            ["O" "X" "O" "X" "O"]
            ["O" "X" "X" "X" "O"]
            ["O" "O" "O" "O" "T"]]
           (-> [["T" "O" "O" "O" "O"]
                ["O" "T" "T" "T" "O"]
                ["O" "T" "O" "T" "O"]
                ["O" "T" "T" "T" "O"]
                ["O" "O" "O" "O" "T"]]
               (fill 3 3 "X"))))))


(deftest format-img-test
  (is (= "012\n345"
         (-> [["0" "1" "2"]
              ["3" "4" "5"]]
          (format-img)))))


(deftest test-parse-command
  (is (= ["xyz" 1 "C"]
         (parse-command {:XYZ ["xyz" [coordinate str]]} "XYZ 1 C"))))
