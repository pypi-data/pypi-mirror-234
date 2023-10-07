![PowerBot Logo](https://www.powerbot-trading.com/wp-content/uploads/2018/03/PowerBot_Weblogo.png "PowerBot")

# **PowerBot Clients**

This repository serves as a way to host and publish PowerBot clients.

### Checklist

The following checklist outlines the necessary steps to take in order to publish a new version of the PowerBot Clients for Python.

1. The auto-update action gets triggered everytime a new version of the PowerBot API spec is published. If changes have been
   detected, a new pull request is created. This PR includes the updated swagger file as well as the corresponding Python clients, which were
   generated with the respective parameterization as seen in the [configs](./configs) directory.
2. Before making a new release, make sure that the clients were built from the correct version of the swagger definition. This can be done by
   verifying that the `version: x.y.z` attribute in changed `swagger.yaml` file.
3. If the version number does not match the expected one, then manually trigger the `Update PowerBot API` action by providing the desired tag of the
   PowerBot backend version in the format `refs/tags/x.y.z`.
4. The setup files automatically extract the version number for the clients from the respective packages. 
5. Tag the latest commit with the corresponding PowerBot version (*git tag <tag_name> <commit_hash>*). This will trigger a GitHub action, which
   automatically uploads both packages to test.pypi.
6. Make sure that the jobs ran successfully. Test that the packages have been published to test.pypi as intended.
7. Create a new release on GitHub. This will trigger a GitHub action, which automatically uploads both packages to the regular pypi.