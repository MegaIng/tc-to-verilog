`timescale 10ns / 1ns

module TC_CheapRamLat_testbench ();
    // clock and reset signals
    reg clk;
    reg rst;

    // dut (Design Under Test) io
    reg load;
    reg save;
    reg [15:0] address;
    reg [15:0] in;
    wire ready;
    wire [15:0] out;
    
    // dut instantiation
    TC_CheapRamLat dut (.clk(clk), .rst(rst), .load(load), .save(save), .address(address), .in0(in), .ready(ready), .out0(out));

    // generate clock
    initial begin
        clk = 1'b0;
        forever #1 clk = ~clk;
    end

    // generate reset
    initial begin
        rst = 1'b1;
        #10
        rst = 1'b0;
    end

    // run tests
    initial begin
        // monitor io
        $monitor("time=%3d, save=%b, load=%b, address=%16b, in=%16b, ready=%b, out=%16b\n",
                    $time, save, load, address, in, ready, out);
        
        // generate all input combinations with 200ns delays
		load = 1'b0;
		save = 1'b0;
		address = 16'b0000_0000_0000_0000;
        in = 16'b0000_0000_0000_0000;
        #25
        address = 16'b0000_0000_0000_0000;
        in = 16'b0000_0000_0000_0001;
        save = 1'b1;
        #20
        save = 1'b0;
        #20
        load = 1'b1;
        #20
        load = 1'b0;
        #20
        address = 16'b0000_0000_0000_0001;
        in = 16'b0000_0000_0000_0010;
        save = 1'b1;
        #20
        save = 1'b0;
        #20
        load = 1'b1;
        #20
        load = 1'b0;
        #20
        address = 16'b0000_0000_0000_0000;
        load = 1'b1;
        #20
        load = 1'b0;
    end
endmodule

