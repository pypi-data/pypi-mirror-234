# tic-tac-toe-backend

<!-- Start SDK Installation -->
## SDK Installation

```bash
pip install tic-tac-toe-backend
```
<!-- End SDK Installation -->

## SDK Example Usage
<!-- Start SDK Example Usage -->
```python
import tic_tac_toe_backends


s = tic_tac_toe_backends.TicTacToeBackends()


res = s.get_()

if res.body is not None:
    # handle response
```
<!-- End SDK Example Usage -->

<!-- Start SDK Available Operations -->
## Available Resources and Operations

### [TicTacToeBackends SDK](docs/sdks/tictactoebackends/README.md)

* [get_](docs/sdks/tictactoebackends/README.md#get_) - Root endpoint.
* [get_version](docs/sdks/tictactoebackends/README.md#get_version) - Root endpoint.
* [put_games](docs/sdks/tictactoebackends/README.md#put_games) - Games endpoint. Creates the next game state from the previous game state.
<!-- End SDK Available Operations -->



<!-- Start Dev Containers -->

<!-- End Dev Containers -->



<!-- Start Pagination -->
# Pagination

Some of the endpoints in this SDK support pagination. To use pagination, you make your SDK calls as usual, but the
returned response object will have a `Next` method that can be called to pull down the next group of results. If the
return value of `Next` is `None`, then there are no more pages to be fetched.

Here's an example of one such pagination call:
<!-- End Pagination -->

<!-- Placeholder for Future Speakeasy SDK Sections -->



### Maturity

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning usage
to a specific package version. This way, you can install the same version each time without breaking changes unless you are intentionally
looking for the latest version.

### Contributions

While we value open-source contributions to this SDK, this library is generated programmatically.
Feel free to open a PR or a Github issue as a proof of concept and we'll do our best to include it in a future release!

### SDK Created by [Speakeasy](https://docs.speakeasyapi.dev/docs/using-speakeasy/client-sdks)
