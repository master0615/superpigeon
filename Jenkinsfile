     // Login to registry
    withCredentials([usernamePassword(credentialsId: 'YOUR_ID_AD_DEFINED_IN_JENKINS', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
        sh "docker login --username=$USER --password=$PASS your.registry.here.com"
    }

    // Build with correct pom version
    sh "docker build -t your.registry.here.com/your_image_here/your_image_name:${POM_VERSION} ."

    // Push
    sh "docker push your.registry.here.com/your_image_here/your_image_name:${POM_VERSION}"

    //pull
    sh "docker pull your.registry.here.com/your_image_here/your_image_name:${POM_VERSION}"