`timescale 10ns / 1ns

module TC_Rom_testbench ();
    // clock and reset signals
    reg clk;
    reg rst;

    // dut (Design Under Test) io
    reg load;
    reg save;
    reg [15:0] address;
    reg [15:0] in;
    wire [15:0] out;
    
    // dut instantiation
    TC_Rom dut (.clk(clk), .rst(rst), .load(load), .save(save), .address(address), .in(in), .out(out));

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
        $monitor("time=%3d, load=%b, save=%b, address=%16b, in=%16b, out=%16b\n",
                    $time, load, save, address, in, out);
        // generate all input combinations with 200ns delays
        load = 1'b1;
        save = 1'b0;
        in = 16'b0000_0000_0000_0000_0000;        
		address = 16'b0000_0000_0000_0000;
        #25
        address = 16'b0000_0000_0000_0001;
        #20
        address = 16'b0000_0000_0000_0010;
        #20
        address = 16'b0000_0000_0000_0011;
        #20
        address = 16'b0000_0000_0000_0100;
        #20
        address = 16'b0000_0000_0000_0101;
        #20
        address = 16'b0000_0000_0000_0110;
        #20
        $finish;
    end
endmodule

