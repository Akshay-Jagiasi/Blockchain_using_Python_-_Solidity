// SPDX-License-Identifier: MIT

//adcoin ICO

//version of the compiler
pragma solidity ^0.8.5;

contract hadcoin_ico{
    //Introducing the maximum number of adcoin available for sale
    uint public max_adcoins = 1000000;

    //Introducing the USD to adcoins conversion rate
    uint public usd_to_adcoins = 1000;  //1 dollar = 1000 adcoins

    //Introducing the total number of adcoins that have been bought by the investors 
    uint public total_adcoins_bought = 0;

    //Mapping from the investors address to its equity in adcoins and USD 
    mapping(address => uint) equity_adcoins;
    mapping(address => uint) equity_usd;
    
    //Checking if an investor can buy adcoins
    modifier can_buy_adcoins(uint usd_invested){
        require (usd_invested * usd_to_adcoins + total_adcoins_bought <= max_adcoins);
        _;
    }

    //Getting the equity in the adcoins of an investor
    function equity_in_usd(address investor) external view returns (uint){
        return equity_usd[investor];
    }
    
    //Buying adcoins
    function buy_adcoins(address investor, uint usd_invested) external 
    can_buy_adcoins(usd_invested){
        uint adcoins_bought = usd_invested*usd_to_adcoins;
        equity_adcoins[investor] += adcoins_bought;      
        equity_usd[investor] = equity_adcoins[investor]/1000;
        total_adcoins_bought += adcoins_bought;  
    }

    //Selling adcoins
    function sell_adcoins(address investor, uint adcoins_sold) external {
        equity_adcoins[investor] -= adcoins_sold;      
        equity_usd[investor] = equity_adcoins[investor]/1000;
        total_adcoins_bought -= adcoins_sold;  
    }
}


// You can run this solidiy code on remix ide for testing